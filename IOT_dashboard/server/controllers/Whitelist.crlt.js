const Whitelist = require("../models/Whitelist.model");
const asyncHandler = require("express-async-handler");


const createWhitelist = async (req, res) => {
    try {
    const license = req.body.email;
    const findWhitelist = await Whitelist.findOne({ license: license });
    if (!findWhitelist) {
      const newWhitelist = await Whitelist.create(req.body);
      console.log(newWhitelist)
      res.send("success");
    } else {
        res.send("whitelist already exists");
    }
  } catch (err) {
    console.log(err);
    res.send(err)
  }
  };

  const fetchWhitelist = async (req, res) => {
    try {
    const Whitelists = await Whitelist.find();
    console.log(Whitelists);
      res.send(Whitelists);
    }
   catch (err) {
    console.log(err);
  }
  };

  
module.exports = {
    createWhitelist,
    fetchWhitelist
};
