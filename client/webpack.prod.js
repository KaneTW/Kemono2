const path = require("path");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const MiniCSSExtractPlugin = require("mini-css-extract-plugin");
// const FaviconsWebpackPlugin = require('favicons-webpack-plugin');
const { merge } = require("webpack-merge");

const baseConfig = require("./webpack.config");

/**
 * @type import("webpack").Configuration
 */
const webpackConfigProd = {
  mode: "production",
  plugins: [
    new CopyWebpackPlugin({
      patterns: [
        {
          from: "static",
          to: "static"
        }
      ]
    }),
    new MiniCSSExtractPlugin({
      filename: "static/css/[name]-[contenthash].css",
      chunkFilename: "static/css/[id]-[contenthash].chunk.css"
    }),
    // new FaviconsWebpackPlugin({
    //   logo:"./src/assets/logo/kemono-logo.svg",
    //   inject: htmlPlugin => path.basename(htmlPlugin.options.filename) === "shell.html",
    //   prefix: "assets/logo"
    // })
  ],
  module: {
    rules: [
      {
        test: /\.m?js$/i,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              [
                '@babel/preset-env', 
                { targets: "defaults" }
              ],
            ],
            plugins: [
              '@babel/plugin-transform-runtime'
            ]
          }
        }
      },
      {
        test: /\.s[ac]ss$/i,
        exclude: /\.module\.s[ac]ss$/i,
        use: [
          MiniCSSExtractPlugin.loader, 
          'css-loader',
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: [
                  ["postcss-preset-env"]
                ]
              }
            }
          },
          "sass-loader"
        ],
      },

      {
        test: /\.(png|svg|jpg|jpeg|gif|webp)$/i,
        type: 'asset/resource',
        generator: {
          filename: "static/assets/[name]-[contenthash][ext][query]"
        }
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        type: 'asset/resource',
        generator: {
          filename: "static/fonts/[name]-[contenthash][ext][query]"
        }
      },
    ]
  },
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "static/js/[name]-[contenthash].bundle.js",
    assetModuleFilename: "static/assets/[name]-[contenthash][ext][query]",
    publicPath: "/",
    clean: true,
  },
  optimization: {
    moduleIds: 'deterministic',
    runtimeChunk: 'single',
    splitChunks: {
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
  }
}

module.exports = merge(baseConfig, webpackConfigProd);