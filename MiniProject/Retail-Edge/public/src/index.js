const express = require('express');
const pasth = require("path");
const bcrypt = require("bcrypt");
const collection = require("./config");
// imported express and other modules
// create an express application
const app = express();
//convert data to json format
app.use(express.json());

app.use(express.urlencoded({extended:false}));

//use EJS as view engine
app.set('view engine','ejs');
//static file

app.use(express.static("public"));

//first parameter is root and second is call back function
//in call back function we have two parameters 1.request and response
//rendering login page 
app.get("/",(req,res)=>{
    res.render("login");
});
//rendering signup page
app.get("/signup",(req,res)=>{
     res.render("signup");

});

//register user
app.post("/signup", async (req,res)=>{
    const data = {
        name:req.body.username,
        password:req.body.password
    }
    //check if user already exists
    const existingUser = await collection.findOne({name: data.name});
    if(existingUser){
        res.send("Username already exists");
    }else{
        //hash the password
        const saltRounds = 10;//number of salt round for bcrypt
        const hashedPassword = await bcrypt.hash(data.password, saltRounds);
      
        data.password = hashedPassword;//replacing hash password with original password

        const userdata = await collection.insertMany(data);
        console.log(userdata);
    }
});

//login user

app.post("/login",async (req,res)=>{
    try{
        const check = await collection.findOne({name:req.body.username});
        if(!check){
           res.send("Username not found");
        }
        //compare the hash password from the database with the plain test
        const isPasswordMatch = await bcrypt.compare(req.body.password , check.password);
        if(isPasswordMatch){
            res.render("home");
        }else{
            req.send("wrong password");
        }
    }
    catch{
           res.send("wrong details");
    }
});

//choose a port to run your application
const port = 5001;
app.listen(port, () => {
    console.log(`Server running on Port: ${port}`);
}) ;