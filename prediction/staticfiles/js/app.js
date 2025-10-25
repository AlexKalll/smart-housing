(function(){
	function toggle(){
		var body = document.body;
		if(body.classList.contains('nav-open')){ body.classList.remove('nav-open'); }
		else { body.classList.add('nav-open'); }
	}
	window.toggleNav = toggle;
})();

