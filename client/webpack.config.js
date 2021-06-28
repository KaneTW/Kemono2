const path = require("path");
// const { WebpackManifestPlugin } = require("webpack-manifest-plugin");

const { buildHTMLWebpackPlugins } = require("./configs/build-templates");

const projectPath = path.resolve(__dirname, "src");
const pagesPath = path.join(projectPath, "pages");
const componentsPath = path.resolve(projectPath, "pages", "components");
const pluginOptions = {
  inject: false,
  minify: false,
};
const pagePlugins = buildHTMLWebpackPlugins(pagesPath, projectPath, pluginOptions);
const componentPlugins = buildHTMLWebpackPlugins(componentsPath, projectPath, pluginOptions);

/**
 * @type import("webpack").Configuration
 */
const webpackConfig = {
  entry: {
    global: path.join(projectPath, "js", "global.js")
  },
  plugins: [
    ...pagePlugins,
    ...componentPlugins,
  ],
  resolve: {
    extensions: [".js"],
    alias: {
      ["@wp/js"]: path.join(projectPath, "js"),
      ["@wp/css"]: path.join(projectPath, "css"),
      ["@wp/pages"]: path.join(projectPath, "pages"),
      ["@wp/assets"]: path.join(projectPath, "assets"),
      ["@wp/api"]: path.join(projectPath, "api", "_index.js"),
    }
  }
}

module.exports = webpackConfig;
