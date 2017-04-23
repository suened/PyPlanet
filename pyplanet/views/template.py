from pyplanet.core.ui.template import load_template
from pyplanet.views.base import View


class TemplateView(View):
	"""
	The TemplateView will provide a view based on a XML template (ManiaLink for example).
	The view contains some class properties that are required to work. Those are described bellow.
	
	To use the TemplateView. Initiate it in your own View class, and override one of the following methods:
	
	:method get_context_data(): Return the global context data here. 
								Make sure you use the super() to retrieve the current context.
	:method get_player_data(): Retrieve the player specific dictionary. 
							   Return dict with player as key and value should contain the data dict.
	:method get_template(): Return the template instance from Jinja2. You mostly should not override this method.
	
	As alternative you can manipulate the instance.data and instance.player_data too.
	
	**Properties that are useful to change**:
	
	:prop data: Global context data. Dict.
	:prop player_data: Player context data. Dict with player as key.
	:prop hide_click: Should the manialink disappear after clicking a button/text.
	:prop timeout: Timeout to hide manialink in seconds.
	
	**Example usage:**
	
	.. code-block:: python

		class AlertView(TemplateView):	
			template_package = 'my_app'
			template_name = 'test.xml' # template should be in: ./my_app/templates/test.xml		
		
			async def get_context_data(self):
				context = await super().get_context_data()
				context['title'] = 'Sample'
				return context

	"""

	template_package = None
	template_name = None

	async def get_context_data(self):
		"""
		Get global and local context data, used to render template.
		"""
		context = dict(
			id=self.id
		)
		return context

	async def get_player_data(self):
		"""
		Get data per player, return dict with login => data dict.
		"""
		return dict()

	async def get_template(self):
		return await load_template(self.template_package, self.template_name)

	async def render(self, *args, player_login=None, **kwargs):
		"""
		:inherit: 
		"""
		kwargs['data'] = await self.get_context_data()
		kwargs['player_data'] = await self.get_player_data()
		kwargs['template'] = await self.get_template()
		return await super().render(*args, **kwargs)