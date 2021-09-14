class Checkup extends ProjectObject { //класс для проверщиков разных параметров
	constructor(options) {
		super(options);
		this.condition = options.condition
		this.ifTrue = options.ifTrue
		this.ifFalse = options.ifFalse
	}

	async infinityCheck(caller) { //бесконечная циклическая асинхронная проверка
		if (caller.condition()) {
			caller.ifTrue();
		}
		else {
			caller.ifFalse();
		}
		setTimeout(caller.infinityCheck, 300, caller); //рекурсивное повторение
	}

	check() { //одноразовая проверка
		if (this.condition(this.$scope, this.$cookies)) {
			this.ifTrue(this.$scope, this.$cookies, this.$timeout);
		}
		else {
			this.ifFalse(this.$scope, this.$cookies, this.$timeout);
		}
		return this;
	}
}