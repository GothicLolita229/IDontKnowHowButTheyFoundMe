using TastyTableLibrary;

namespace WebAppUI.Models
{
	public class Recipe
	{
		public int Id { get; set; }
		public string Name { get; set; }
		public List<Ingredient> Ingredients { get; set; }
		public List<Instruction> Instructions { get; set; }
		public int Temperature { get; set; }

		public Recipe()
		{

		}
	}
}
