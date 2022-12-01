module.exports = {
    devServer: {
        port: 3000,
        proxy: {
            '/jsonplaceholder': {
                target: 'http://jsonplaceholder.typicode.com',
                secure: false,
                pathRewrite: {
                    '^/jsonplaceholder': ''
                }
            },
            '/api': {
                target: 'http://127.0.0.1:5000',
                secure: false,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    },
    configureWebpack: {
        devtool: 'source-map'
    }
}