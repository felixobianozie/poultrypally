// Mobile navigation menu control
function showMobileMenu(){
    var x = document.getElementById("mobile_menu");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else { 
        x.className = x.className.replace(" w3-show", "");
    }
}

// Tab navigation menu control
function showTabMenu(){
    var x = document.getElementById("tab_menu");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else { 
        x.className = x.className.replace(" w3-show", "");
    }
}

// Highlight the active tab
activeTab();

function activeTab(){
    var tmp1 = document.getElementsByTagName("title");
    var tmp2 = document.getElementsByClassName("left_nav");

    for(let i = 0; i < tmp2.length; i++){
         if (tmp2[i].innerHTML.toLowerCase().indexOf(tmp1[0].innerHTML.toLowerCase()) != -1){
            tmp2[i].className = "left_nav w3-lime w3-hover-gray";
         }
    }
}

// Responsive Batch Details
function showDetails(){
    var a = document.getElementById("batch_details");
    var b = document.getElementById("details_btn");
    var c = document.getElementById("main");
    var d = document.getElementById("batch_details_mobile");
    var e = document.getElementById("left_nav_bar");
    

    a.className = "w3-col m4 l3 w3-container w3-padding-16 w3-black w3-section \
        summary w3-animate-right w3-hide-small w3-show-medium w3-show-large";
    b.className = "w3-black w3-container summary w3-button w3-hide w3-animate-right";
    c.className = "w3-col m6 l6";
    d.className = "w3-col m4 l3 w3-container w3-padding-16 w3-black w3-section \
        w3-round-large w3-animate-right w3-show-small w3-hide-medium w3-hide-large";
    e.className = "w3-col m2 l3";

}

function hideDetails(){
    var a = document.getElementById("batch_details");
    var b = document.getElementById("details_btn");
    var c = document.getElementById("main");
    var d = document.getElementById("batch_details_mobile");
    var e = document.getElementById("left_nav_bar");

    a.className = "w3-col m4 l3 w3-container w3-padding-16 w3-black w3-section \
        summary w3-animate-right w3-hide-small w3-hide-medium w3-hide-large";
    b.className = "w3-black w3-container summary w3-button w3-show w3-animate-right";
    c.className = "w3-col m9 l9";
    d.className = "w3-col m4 l3 w3-container w3-padding-16 w3-black w3-section \
        w3-round-large w3-animate-right w3-hide-small w3-hide-medium w3-hide-large";
    e.className = "w3-col m3 l3";
}


