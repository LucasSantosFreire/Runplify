from jupyter_server.base.handlers import JupyterHandler
import tornado
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

class RunplifyHandler(JupyterHandler):
    @tornado.web.authenticated
    def post(self):
        request = self.get_json_body()
        host = "smtp.gmail.com"
        port = "587"
        error_handler = False
        file_path = os.path.abspath(request["path"])
        env_directory = os.path.dirname(file_path)
        load_dotenv(env_directory + "/.env")
        email = os.getenv("EMAIL")
        passw = os.getenv("PASSWORD")
        with open(file_path) as f:
            nb = nbformat.read(f, as_version=4)    
            ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
            try:
                out = ep.preprocess(nb)
            except CellExecutionError:
                out = None
                error_handler = True
            finally:            
                with open(env_directory + '/executed_notebook.ipynb', 'w', encoding='utf-8') as f:
                    nbformat.write(nb, f)
        server = smtplib.SMTP(host, port)
        server.starttls()        
        server.login(email, passw)
        if(error_handler == False):
            body = 'Your code has finished running, your results have been saved in the execute_notebook file.'
            subject = 'Your code has finished running!'
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            arq_path = env_directory + '/executed_notebook.ipynb'
            arq_bin = open(arq_path, 'rb')           
            attach_core = MIMEBase('application', 'octet-stream')
            attach_core.set_payload(arq_bin.read())
            encoders.encode_base64(attach_core)              
            attach_core.add_header('Content-Disposition', 'attachment', filename='executed_notebook.ipynb')
            arq_bin.close()
            msg.attach(attach_core)
            server.sendmail(msg['To'], msg['From'], msg.as_string())
        elif(error_handler == True):
            body = 'Your code has finished running with some erros, check your results  in the executed_notebook file.'
            subject = 'Your code has finished running with some errors!'
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            arq_path = env_directory + '/executed_notebook.ipynb'
            arq_bin = open(arq_path, 'rb')           
            attach_core = MIMEBase('application', 'octet-stream')
            attach_core.set_payload(arq_bin.read())
            encoders.encode_base64(attach_core)              
            attach_core.add_header('Content-Disposition', 'attachment', filename='executed_notebook.ipynb')
            arq_bin.close()
            msg.attach(attach_core)
            server.sendmail(msg['To'], msg['From'], msg.as_string())                     
        server.quit()
        self.write("OK")