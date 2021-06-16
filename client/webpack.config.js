const path = require("path");
const HTMLWebpackPlugin = require("html-webpack-plugin");
// const { WebpackManifestPlugin } = require("webpack-manifest-plugin");

const templatePath = {
  base(name) {
    return "pages/" + name + ".html"
  }, 
  components(name) {
    return "pages/components/" + name + ".html"
  }
}

/**
 * @type import("webpack").Configuration
 */
const webpackConfig = {
  entry: {
    index: "./src/js/index.js"
  },
  plugins: [
    // components
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("artist_list"),
      filename: templatePath.components("artist_list"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("card"),
      filename: templatePath.components("card"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("flash_messages"),
      filename: templatePath.components("flash_messages"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("header"),
      filename: templatePath.components("header"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("help_sidebar"),
      filename: templatePath.components("help_sidebar"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("import_sidebar"),
      filename: templatePath.components("import_sidebar"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("paginator"),
      filename: templatePath.components("paginator"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("post_list"),
      filename: templatePath.components("post_list"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("post_view"),
      filename: templatePath.components("post_view"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("preview"),
      filename: templatePath.components("preview"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("shell"),
      filename: templatePath.components("shell"),
      chunks: ["index"],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("subheader"),
      filename: templatePath.components("subheader"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.components("thumb"),
      filename: templatePath.components("thumb"),
      chunks: [],
      minify: false
    }),
    // pages
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("about"),
      filename: templatePath.base("about"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("account"),
      filename: templatePath.base("account"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("artists"),
      filename: templatePath.base("artists"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("bans"),
      filename: templatePath.base("bans"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("blocked"),
      filename: templatePath.base("blocked"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("board_list"),
      filename: templatePath.base("board_list"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("discord"),
      filename: templatePath.base("discord"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("error"),
      filename: templatePath.base("error"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("favorites"),
      filename: templatePath.base("favorites"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("help_list"),
      filename: templatePath.base("help_list"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("help_posts"),
      filename: templatePath.base("help_posts"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("home"),
      filename: templatePath.base("home"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("importer_list"),
      filename: templatePath.base("importer_list"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("importer_ok"),
      filename: templatePath.base("importer_ok"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("importer_status"),
      filename: templatePath.base("importer_status"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("importer_tutorial"),
      filename: templatePath.base("importer_tutorial"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("license"),
      filename: templatePath.base("license"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("login"),
      filename: templatePath.base("login"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("post"),
      filename: templatePath.base("post"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("posts"),
      filename: templatePath.base("posts"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("register"),
      filename: templatePath.base("register"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("requests_list"),
      filename: templatePath.base("requests_list"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("requests_new"),
      filename: templatePath.base("requests_new"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("requests_snippet"),
      filename: templatePath.base("requests_snippet"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("rules"),
      filename: templatePath.base("rules"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("success"),
      filename: templatePath.base("success"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("updated"),
      filename: templatePath.base("updated"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("upload"),
      filename: templatePath.base("upload"),
      chunks: [],
      minify: false
    }),
    new HTMLWebpackPlugin({
      template: "./src/" + templatePath.base("user"),
      filename: templatePath.base("user"),
      chunks: [],
      minify: false
    }),    
  ],
  resolve: {
    extensions: [".js"],
    alias: {
      ["@wp/js"]: path.resolve(__dirname, "src/js"),
      ["@wp/css"]: path.resolve(__dirname, "src/css"),
      ["@wp/pages"]: path.resolve(__dirname, "src/pages"),
      ["@wp/assets"]: path.resolve(__dirname, "src/assets"),
    }
  }
}

module.exports = webpackConfig;