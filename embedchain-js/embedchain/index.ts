import { EmbedChainApp } from './embedchain';
/**
 * Initializes and returns an instance of the EmbedChainApp.
 *
 * @returns {Promise<EmbedChainApp>} A promise that resolves to an instance of the EmbedChainApp.
 */
export const App = async () => {
  const app = new EmbedChainApp();
  await app.initApp;
  return app;
};