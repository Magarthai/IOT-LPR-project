const mongoose = require('mongoose');

let dashboardSchema = new mongoose.Schema({
    type:{
        type: String,
        required: true
    }
}, { timestamps: true });

module.exports = mongoose.model('dashboards', dashboardSchema);