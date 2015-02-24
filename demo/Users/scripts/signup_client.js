/* TITLE   | Users API Client
 * AUTHOR  | Hunter John Larco
 * VERSION | 0.0.0
*/
(function(){
	
	// NEVER change the CLIENT_SALT
	const CLIENT_SALT = '(*$NBF@'
	const URL_SCHEME = new RegExp('^users.signup:(.*)$')
	
	// Finds all forms with a login url
	function FindForms(){
		var forms = document.getElementsByTagName('form');
		for(var i=0,form; form=forms[i++];){
			var dest = form.getAttribute('action'),
					matches_scheme = URL_SCHEME.test(dest);
			if(!matches_scheme) continue;
			BindSignupForm(form);
		}
	}
	
	function BindSignupForm(form){
		var dest = form.getAttribute('action'),
				matches = dest.match(URL_SCHEME),
				redirect = matches[1];
		form.addEventListener('submit', function(){
			SetupSignupParameters(form);
		});
		form.setAttribute('method', 'POST');
		form.setAttribute('action', redirect)
	}
	
	function SetupSignupParameters(form, redirect){
		var password = form.password.value;
		password = Sha256.hash(CLIENT_SALT + password);
		password = password.slice(-3) + password.slice(0,-3);
		form.password.removeAttribute('name');
		form.appendChild(CreateHiddenInput('password', password));
	}
	
	function CreateHiddenInput(name, value){
		var input = document.createElement('input');
		input.setAttribute('name', name);
		input.value = value;
		input.style.display = 'none';
		return input;
	}
	
	function Init(){
		FindForms();
	}
	
	window.addEventListener('load', Init);
	
})();