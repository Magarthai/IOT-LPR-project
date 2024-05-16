const express = require("express");
const {
    createWhitelist,
    fetchWhitelist
} = require("../controllers/Whitelist.crlt");
const { authMiddleware, isAdmin } = require("../middlewares/authMiddleware");

const router = express.Router();

router.post('/createWhitelist',createWhitelist);
router.get('/getWhitelist', fetchWhitelist);

module.exports = router;
