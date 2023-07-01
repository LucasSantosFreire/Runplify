import { IDisposable, DisposableDelegate } from '@lumino/disposable';

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';
import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { ToolbarButton } from '@jupyterlab/apputils';
import { runIcon } from '@jupyterlab/ui-components';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import {
  NotebookPanel,
  INotebookModel,
} from '@jupyterlab/notebook';

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'Runplify',
  autoStart: true,
  activate: (
    app: JupyterFrontEnd,
  ) => {
    app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());
  }
};


export class ButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>,
  ): IDisposable {
    const click = async () => {
      alert("Runplify is running!")
      const data = { path: context.path}
      let settings = ServerConnection.makeSettings({});
      let serverResponse = await ServerConnection.makeRequest(
        URLExt.join(settings.baseUrl, '/runplify'), { method: 'POST', body: JSON.stringify(data)}, settings);
      console.log(serverResponse);
    };
    const button = new ToolbarButton({
      className: 'runplify-button',
      label: 'Runplify',
      icon: runIcon,
      onClick: click,
      tooltip: 'Runplify',
    });
     
    panel.toolbar.insertItem(10, 'Runplify', button);
    return new DisposableDelegate(() => {
      button.dispose();
    });
  }
}

export default plugin;