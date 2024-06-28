function toggleSection(sectionId) {
    var section = document.getElementById(sectionId);
    if (section.classList.contains('hidden')) {
        section.classList.remove('hidden');
        section.classList.add('slide-in');
    } else {
        section.classList.remove('slide-in');
        section.classList.add('hidden');
    }
}