const path = require("path");
const fse = require("fs-extra");
const HTMLWebpackPlugin = require("html-webpack-plugin");

/**
 * Builds an array of HTML webpack plugins from the provided folder.
 * @param {string} basePath An absolute path to the folder containing template files.
 * @param {string} projectPath An absolute path to the folder containing project files.
 * @param {HTMLWebpackPlugin.Options} options HTMLWebpackPlugin options.
 */
function buildHTMLWebpackPlugins(basePath, projectPath, options) {
  /**
   * @type {HTMLWebpackPlugin[]}
   */
  const plugins = [];
  const files = fse.readdirSync(basePath, { withFileTypes: true });

  files.forEach(( file ) => {
    const isHTML = file.isFile() && file.name.endsWith(".html");
    
    if (isHTML) {
      const templatePath = path.join(basePath, file.name);
      const outputBase = path.relative(projectPath, basePath);
      const outputPath = path.join(outputBase, file.name);

      const webpackPlugin = new HTMLWebpackPlugin({
        ...options,
        template: templatePath,
        filename: outputPath,
      });

      plugins.push(webpackPlugin);
    }
  });

  return plugins;
}

module.exports = {
  buildHTMLWebpackPlugins
}
