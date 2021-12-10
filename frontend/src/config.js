import Cookies from 'js-cookie'

var config = {};

function updateConfig(force = false, engine = 'reddit', searxURL = 'http://127.0.0.1:5002/search'){
    if(!Cookies.get('engine') || force){
        Cookies.set('engine', engine);
    }
    Cookies.set('searxURL', searxURL);

    config = {
        "engine": Cookies.get('engine'),
        "searxURL" : Cookies.get('searxURL'),
    }
    if(force){
    window.location.reload()
    }
}

updateConfig();

console.log(config)

export default config
export {updateConfig}