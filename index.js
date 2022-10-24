const fs = require('fs');
const transformer = require('enketo-transformer');

const config = {
  inputDir: 'data-xml',
  outputDir: 'data-json',
};

console.log('==== xform-transformer ====');
console.log('');
console.log(`Input directory: "${config.inputDir}"`);
console.log(`Output directory: "${config.outputDir}"`);
console.log('');
console.log('Begin transforming xform files...');
console.log('');

fs.readdirSync(`./${config.inputDir}`, {
  encoding: 'utf8',
  withFileTypes: true,
}).filter(file => {
  return file.name.match(/.xml$/);
}).forEach(file => {
  const filename = file.name.substring(0, file.name.length - 4);
  const inputPath = `/user/src/app/${config.inputDir}/${file.name}`;
  const outputPath = `/user/src/app/${config.outputDir}/${filename}.json`;
  console.log(`Reading "${inputPath}" ...`);
  transformer.transform({
    xform: fs.readFileSync(inputPath),
    preprocess: doc => doc,
  }).then(function(result){
    fs.writeFileSync(outputPath, JSON.stringify(result));
    console.log(`Successfully saved "${outputPath}"`);
  });
});

