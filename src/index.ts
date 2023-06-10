import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

/**
 * Initialization data for the runplify extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'runplify:plugin',
  description: 'A Juupyter lab extension to save execution output',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension runplify is activated!');
  }
};

export default plugin;
