const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  chainWebpack: config => {
    config
      .plugin('html')
      .tap(args => {
        args[0].title = 'A five-in-a-row Game with AI!'
        return args
      })
  },
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production' ? './' : './',

  // 👇 关键修改：打包输出到后端的 static 文件夹
  outputDir: path.resolve(__dirname, '../../back-end/static'),
  assetsDir: '',
  configureWebpack: {
    performance: {
      hints: false
    }
  }
})
