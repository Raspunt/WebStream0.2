
const { createApp } = Vue


try{
Vue.config.devtools = true;
}
catch (e){
 console.log('dev-tools not work ):')
}

let app = createApp({
   data() {
     return {
       showVideo:true,
       username:"",
       password:"",
       ImgDegrees:90
     }
   },
 methods:{
    

    CheckUser(){
        var fd = new FormData();
        fd.append('username', this.username);
        fd.append('password', this.password);
    
        axios({
            method: "post",
            url: "/LoginUser",
            data:fd,
            headers: { "Content-Type": "multipart/form-data" },
            })
        .then(function (response) {
            //handle success
            console.log(response.data);

            if (response.data === "correct"){
                app.showVideo = true;
                console.log(app.showVideo);
                
            }


        })
        .catch(function (response) {
            //handle error
        });	
    },
    RotateCamera(){
        
        const camera = document.getElementById('camera');
        camera.style.transform = `rotate(${this.ImgDegrees}deg)`;
        this.ImgDegrees += 90

    },

    StopCamera(){

        axios({
            method: "post",
            url: "/stopCamera",
            headers: { "Content-Type": "multipart/form-data" },
        })
        .then((response)=>{

        })

        console.log("Stop Camera");

    },

    StartCamera(){
        // axios({
        //     method: "post",
        //     url: "/startCamera",
        //     headers: { "Content-Type": "multipart/form-data" },
        // })
        // .then((response)=>{

        // })


        location.reload(); 
        console.log("Start Camera");

    }
    
},
created(){
    setInterval(()=>{
        if (app.showVideo == true){
            
            
            axios({
                url: "/temp",
                headers: { "Content-Type": "multipart/form-data" },
            })
            .then(function (response) {
                // console.log(response.data);
                let  temp = document.getElementById('temp')
                temp.innerHTML = 'температура:'+response.data
                
            })
            .catch(function (response) {
                // console.log(response); 
            });	
            
        }
    },2000)
}

}).mount('#app')
