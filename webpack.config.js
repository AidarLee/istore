const path = require('path');
module.exports = {
  entry: path.resolve(__dirname, 'src/app.js'),
  output: {
    filename: 'app.js',
    path: path.resolve(__dirname, 'webapp/static/js')
  },
  module: {
      rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  }
};