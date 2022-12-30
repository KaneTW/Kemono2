const path = require("path");

const MiniCSSExtractPlugin = require("mini-css-extract-plugin");
const { merge } = require("webpack-merge");

const baseConfig = require("./webpack.config");
const { kemonoSite } = require("./configs/vars");
/**
 * @type import("webpack").Configuration
 */
const webpackConfigProd = {
  mode: "production",
  // devtool: "source-map",
  plugins: [
    new MiniCSSExtractPlugin({
      filename: "static/bundle/css/[name]-[contenthash].css",
      chunkFilename: "static/bundle/css/[id]-[contenthash].chunk.css"
    })
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
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.s[ac]ss$/i,
        exclude: /\.module\.s[ac]ss$/i,
        use: [
          MiniCSSExtractPlugin.loader,
          {
            loader: 'css-loader',
            // options: {
            //   sourceMap: true,
            // }
          }, 
          
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
          {
            loader: "sass-loader",
            options: {
              // sourceMap: true,
              additionalData: `$kemono-site: '${kemonoSite}';`
            }
          }
          
        ],
      },

      {
        test: /\.(png|jpg|jpeg|gif|webp)$/i,
        type: 'asset/resource',
        generator: {
          filename: "static/bundle/assets/[name]-[contenthash][ext][query]"
        }
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        type: 'asset/resource',
        generator: {
          filename: "static/bundle/fonts/[name]-[contenthash][ext][query]"
        }
      },
      {
        test: /\.svg$/i,
        type: 'asset/resource',
        generator: {
          filename: "static/bundle/svg/[name]-[contenthash][ext][query]"
        }
      },
    ]
  },
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "static/bundle/js/[name]-[contenthash].bundle.js",
    assetModuleFilename: "static/bundle/assets/[name]-[contenthash][ext][query]",
    // sourceMapFilename: "source-maps/[file].map[query]",
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
