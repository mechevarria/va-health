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
                target: 'http://localhost:5000',
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