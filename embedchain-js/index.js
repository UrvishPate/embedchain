const { EmbedChainApp } = require("./embedchain/embedchain");
/**
 * Asynchronously initializes and returns an instance of the EmbedChainApp.
 *
 * @async
 * @function
 * @returns {Promise<EmbedChainApp>} A promise that resolves to an instance of EmbedChainApp.
 */
async function App() {
  const app = new EmbedChainApp();
  await app.init_app;
  return app;
}
module.exports = { App };