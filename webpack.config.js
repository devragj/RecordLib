const path = require("path")
const BundleTracker = require('webpack-bundle-tracker')

//login: './frontend/src/login/index',

const config = {
    context: __dirname,
    entry: {
        home: './frontend/src/index.js',
    },
    output: {
        path: path.resolve('./frontend/bundles/'),
        filename: "[name]-[hash].js",
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
    ],
    module: {
        rules: [
            { 
                test: /\.jsx?$/, 
                exclude: /node_modules/, 
                loader: 'babel-loader',
            },
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    {
                        loader: 'css-loader',
                        options: {
                            importLoaders: 1
                        }
                    }
                ]
            }, 
        ],
    },
    resolve: {
        modules: ['node_modules'],
        extensions: ['.js', '.jsx'],
    },
}



module.exports = config