class Button extends ProjectObject {
    constructor(options) {
        super(options);
        this.id = options.id
        this.domObj = document.getElementById(this.id);
        this.clickFunction = options.clickFunction
        return this;
    }

    disabled() {
        this.domObj.disabled = true
        return this;
    }

    enabled() {
        this.domObj.disabled = false
        return this;
    }

    click() {
        this.clickFunction(this.$cookies);
    }
}