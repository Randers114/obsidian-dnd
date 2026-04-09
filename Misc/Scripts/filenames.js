const fs = require('fs');
const path = require('path');

/**
 * Get all filenames from the current script's directory.
 * @returns {string[]} - Array of filenames.
 */
function getFilenames() {
    const folderPath = __dirname;
    console.log(folderPath)
    try {
        return fs.readdirSync(folderPath).map(file => path.join(folderPath, file));
    } catch (error) {
        console.error("Error reading directory:", error);
        return [];
    }
}

console.log("This")
// Example usage:
console.log(getFilenames());

module.exports = getFilenames;
