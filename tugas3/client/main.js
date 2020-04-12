const express = require('express');
const app = express();


app.get('/', (req,res)=> {
  res.sendFile(__dirname + "/home.html")
});

// app.post('/api/compress', (req,res)=>{
//   console.log("request",req);
//   console.log("response", res);
  
// });

app.listen(20744, ()=>{
  console.log("Working on port 20744");
});

