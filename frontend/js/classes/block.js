class Block extends ProjectObject {
	constructor(options) {
		super(options);
		this.id = options.id
		this.domObj = document.getElementById(this.id);
		return this;
	}
	
	hidden() {
		this.domObj.style.display = "none";
		return this;
	}

	view() {
		this.domObj.style.display = "block";
		return this;
	}
}