function toQueryString(params){
    return new URLSearchParams(params).toString();
}

function keywordToQueryString(keywords){
    var result = ''
    for(const key of keywords){
        const subkey = key.toString().split(" ");
        if(subkey.length > 1){
            result += `"${key}"`;  
        }
        else{
            result += `${key}`
        }
        result += " ";
    }
    return result;
}

export {toQueryString, keywordToQueryString}