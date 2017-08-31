angular.module("Playground")
.controller("ContactController", function(){
	this.contacts = [
		{
			name:"Al Gore",
			lastMsg:"Sounds good!"
		},

		{
			name:"Dank Master Dunk",
			lastMsg:"Ghadda go fast"
		},

		{
			name:"Bill Nye",
			lastMsg:"Better reply thoughtfully to this one"
		},

		{
			name:"Neil D. Tyson",
			lastMsg:"People say the universe don't be how it is but it do"
		}
	]
});