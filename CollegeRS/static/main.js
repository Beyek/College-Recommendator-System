var hiddenClass = 'hidden';
var shownClass = 'toggled-from-hidden';

function collegeSectionHover() {
    var children = this.children;
    for(var i = 0; i < children.length; i++) {
        var child = children[i];
        if (child.className === hiddenClass) {
            child.className = shownClass;
        }
    }
}

function petSectionEndHover() {
    var children = this.children;
    for(var i = 0; i < children.length; i++) {
        var child = children[i];
        if (child.className === shownClass) {
            child.className = hiddenClass;
        }
    }
}

(function() {
    var petSections = document.getElementsByClassName('colzrRS');
    for(var i = 0; i < petSections.length; i++) {
        petSections[i].addEventListener('mouseover', collegeSectionHover);
        petSections[i].addEventListener('mouseout', petSectionEndHover);
    }
}());
