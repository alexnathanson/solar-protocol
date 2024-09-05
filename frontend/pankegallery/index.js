var paragraphs = document.querySelectorAll(".date p");
var currentTime;
var currentHour;
var currentDateString; 
var currentDateStringCleaned; 

var nowParagraph = document.getElementById("now");
var color = "black";

var isAutoScrolling = false;

var resizeTimeout;

var startY = 0;

document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        document.getElementById('mainimage').classList.add('hidden');
    }, 2000); 
  });

// standardize time input
function getCurrentDateTime() {
    const now = new Date();
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short'
    };
    const formatter = new Intl.DateTimeFormat('en-GB', options);
    return formatter.format(now);
}
  
function setCurrentTime() {
    const time = getCurrentDateTime();
    currentTime=time;
    currentHour=new Date().getHours();
    currentDateString = currentTime.toLocaleString().substring(0, 20);// '01/06/2024, 16:00:00'; 
    nowParagraph.innerHTML = currentDateString;
    currentDateStringCleaned = currentDateString.substring(0, 10); 
}

window.onload = setCurrentTime();

function checkWindowSize() {
    var windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

    if (windowWidth < 1100) {
        if (window.location.href.indexOf("mobile.html") === -1) {
            window.location.href = 'mobile.html';  
        }
    } else {
        if (window.location.href.indexOf("index.html") === -1) {
            window.location.href = 'index.html';         
        }
    }
}

function toggleOverlay() {
    var overlay = document.getElementById('overlay');
    var aboutwrapper = document.getElementById('about-wrapper');
    overlay.style.display = overlay.style.display === 'block' ? 'none' : 'block';
    document.body.style.overflow = overlay.style.display === 'none' ? 'auto' : 'hidden';
}

document.querySelector('.about').addEventListener('click', toggleOverlay);

document.getElementById('closeButton').addEventListener('click', toggleOverlay);

function throttleResize() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(checkWindowSize, 200);
}

checkWindowSize();
window.addEventListener('resize', throttleResize);

function handleAutoScroll() {
    isAutoScrolling = true;
    window.removeEventListener('scroll', handleAutoScroll); 
}

function handleManualScroll() {
    if (!isAutoScrolling) {
        nowParagraph.innerHTML = '˚. ✦.˳·✶ ⋆ happening now ˚. ✦.˳·✶ ⋆';
        nowParagraph.style.setProperty('--horizontalline-color', 'rgb(85, 85, 85, 0)');
    }
    isAutoScrolling = false; 
}

function onTouchStart(event) {
    startY = event.touches[0].clientY;
}

function onTouchMove(event) {
    var deltaY = event.touches[0].clientY - startY;
    if (Math.abs(deltaY) > 1) { 
        nowParagraph.innerHTML = '˚. ✦.˳·✶ ⋆ happening now ˚. ✦.˳·✶ ⋆' ;
        nowParagraph.style.setProperty('--horizontalline-color', 'rgb(85, 85, 85, 0)');
    }
}

window.addEventListener('scroll', handleAutoScroll);
window.addEventListener('wheel', handleManualScroll);
window.addEventListener('touchstart', onTouchStart);
window.addEventListener('touchmove', onTouchMove);

function resetAndScroll() {
    var lastParagraphHourString = "0";
    nowParagraph.innerHTML = currentDateString;
    nowParagraph.style.setProperty('--horizontalline-color', 'rgb(85, 85, 85, 1)');
    for (var i = 0; i < paragraphs.length; i++) {
        var paragraphDateString = paragraphs[i].innerText.substring(0, 10); // Extract day, month, and year
        var paragraphHourString = paragraphs[i].innerText.substring(12, 14); // Extract hour
        if (paragraphDateString === currentDateStringCleaned) {
            if ((paragraphDateString === "01/06/2024" || paragraphDateString === "02/06/2024" )) { //|| paragraphDateString === "07/09/2024" || paragraphDateString === "08/09/2024" || paragraphDateString === "22/09/2024" || paragraphDateString === "29/09/2024" || paragraphDateString === "06/10/2024" || paragraphDateString === "10/10/2024" || paragraphDateString === "11/10/2024"
                lastParagraphHourString = paragraphHourString;
                if(paragraphHourString >= currentHour &&  lastParagraphHourString > currentHour) {
                // Include hours in the comparison
                paragraphs[i-1].scrollIntoView({ behavior: "smooth", block: "center" }); 
                    break;
                }
            }
            else { 
                paragraphs[i].scrollIntoView({ behavior: "smooth", block: "center" }); 
                break;
            }
        }
    }
}

nowParagraph.addEventListener('click',() => {    
        setCurrentTime(); 
        resetAndScroll();
           
    });

resetAndScroll();



