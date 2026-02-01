const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/main.jsx',           // ← change to './src/index.jsx' or './src/index.js' if your file has different name
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    clean: true,
    publicPath: '/',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: { loader: 'babel-loader' },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      // Ensure single React instance for all packages
      'react': path.resolve(__dirname, 'node_modules/react'),
      'react-dom': path.resolve(__dirname, 'node_modules/react-dom'),
    },
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './index.html',      // ← change to './public/index.html' if your HTML is in public folder
    }),
  ],
  devServer: {
    static: { directory: path.join(__dirname, 'dist') },
    historyApiFallback: true,
    hot: true,
    port: 3000,
    open: true,
  },
  mode: 'development',   // will be overridden by command
};