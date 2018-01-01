export let model = {}
class Program{
	constructor(name) {
		this.name = name
		this.variables = []
	}
	Variable(name) {
		this.variables.append(name)
	}
}
model.program = (name) => Program(name)