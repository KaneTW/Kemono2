// const FaviconsWebpackPlugin = require("favicons-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require("path");
const { merge } = require("webpack-merge");

const baseConfig = require("./webpack.config");

/**
 * @type {import("webpack-dev-server").Configuration}
 */
const devServer = {
  host: "0.0.0.0",
  port: 3450,
  writeToDisk: true,
  watchOptions: {
    poll: 500,
    aggregateTimeout: 500
  },
  publicPath: "/",
  contentBase: path.resolve(__dirname, "static"),
  watchContentBase: true,
  hot: false,
}

/**
 * @type import("webpack").Configuration
 */
const webpackConfigDev = {
  mode: "development",
  devtool: "inline-source-map",
  devServer: devServer,
  plugins: [
    new MiniCssExtractPlugin({
      filename: "static/css/[name].css",
      chunkFilename: "static/css/[id].chunk.css"
    }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: "static",
          to: "static"
        }
      ]
    }),
    
    // new FaviconsWebpackPlugin({
    //   logo:"./src/assets/logo/kemono-logo.svg",
    //   inject: htmlPlugin => path.basename(htmlPlugin.options.filename) === "shell.html",
    //   prefix: "static/assets/logo"
    // })
  ],
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,
        exclude: /\.module.s[ac]ss$/i,
        use: [
          MiniCssExtractPlugin.loader, 
          'css-loader',
          'sass-loader'
        ],
      },
      {
        test: /\.(png|jpg|jpeg|gif|webp|svg)$/i,
        type: 'asset/resource',
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        type: 'asset/resource',
      },
    ]
  },
  output: {
    path: path.resolve(__dirname, "dev"),
    filename: "static/js/[name].bundle.js",
    assetModuleFilename: "static/assets/[name][ext][query]",
    clean: true,
  }
}

module.exports = merge(baseConfig, webpackConfigDev);