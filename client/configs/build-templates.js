const path = require("path");
const fse = require("fs-extra");
const HTMLWebpackPlugin = require("html-webpack-plugin");

/**
 * @typedef BuildOptions
 * @property {string} fileExtension
 * @property {string} outputPrefix
 * @property {HTMLWebpackPlugin.Options} pluginOptions Webpack plugin options.
 */

/** */
class TemplateFile {
  /**
   * @param {fse.Dirent} dirent 
   * @param {string} path Absolute path to the file.
   */
  constructor(dirent, path) {
    this.dirent = dirent;
    this.path = path;
  }
}

/**
 * Builds an array of HTML webpack plugins from the provided folder.
 * @param {string} basePath Absolute path to the template folder.
 * @param {BuildOptions} options Build optons.
 */
 function buildHTMLWebpackPluginsRecursive(basePath, options) {
  /**
   * @type {HTMLWebpackPlugin[]}
   */
  const plugins = [];
  const files = walkFolder(basePath);

  files.forEach(( file ) => {
    const isTemplateFile = file.dirent.isFile() && file.path.endsWith(`${options.fileExtension}`);

    if (isTemplateFile) {
      const outputBase = path.relative(basePath, file.path);
      const outputPath = path.join(path.basename(basePath), outputBase);

      const webpackPlugin = new HTMLWebpackPlugin({
        ...options.pluginOptions,
        template: file.path,
        filename: outputPath,
      });
  
      plugins.push(webpackPlugin);
    }

  });

  return plugins;
}

/**
 * @param {string} folderPath Absolute path to the folder.
 * @param {TemplateFile[]} files
 */
function walkFolder(folderPath, files = [], currentCount = 0) {
  const nestedLimit = 1000;
  const folderContents = fse.readdirSync(folderPath, {withFileTypes: true});

  folderContents.forEach((entry) => {
    const file = entry.isFile() && entry;
    const folder = entry.isDirectory() && entry;

    if (file) {
      const filePath = path.join(folderPath, file.name);
      files.push(new TemplateFile(file, filePath));
      return;
    }

    if (folder) {
      currentCount++;

      if (currentCount > nestedLimit) {
        throw new Error(`The folder at "${folderPath}" contains more than ${nestedLimit} folders.`);
      }

      const newFolderPath = path.join(folderPath, folder.name);

      return walkFolder(newFolderPath, files, currentCount);
    }

  });

  return files;
}

module.exports = {
  buildHTMLWebpackPluginsRecursive
}
