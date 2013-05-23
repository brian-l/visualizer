$ ->
	vis.init()

vis =
	sys: arbor.ParticleSystem(1000, 400, 1)

	init: ->
		vis.sys.parameters({gravity: true})
		vis.sys.renderer = Renderer("#viewport")
		vis.getProcesses()

	getProcesses: ->
		$.ajax
			type: 'GET'
			url: '/processes'
			data: {}
			success: (response, status,xhr) ->
				vis.sys.merge(response)
				window.setTimeout (->
					vis.getProcesses()), 5000

		
