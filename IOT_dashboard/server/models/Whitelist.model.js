const mongoose = require('mongoose');

let list_whitelistSchema = new mongoose.Schema({
    name:{
        type: String,
        required: true
    },
    license:{
        type: String,
        required: true
    }
}, { timestamps: true });

module.exports = mongoose.model('list_whitelists', list_whitelistSchema);