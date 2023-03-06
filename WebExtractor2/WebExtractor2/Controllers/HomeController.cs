using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System.Data;
using MySql.Data.MySqlClient;
using WebExtractor2.Models;
using System.Diagnostics;

namespace WebExtractor2.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index()
        {
            // Connection string for MySQL database
            string connStr = "server=localhost;user=root;database=newsextractdb;port=3306;password=Hs02209374%";

            // SQL query to retrieve data from database
            string sql = "SELECT title, summary, link, published, topic FROM dataset";

            using (MySqlConnection conn = new MySqlConnection(connStr))
            {
                using (MySqlCommand cmd = new MySqlCommand(sql, conn))
                {
                    conn.Open();
                    using (MySqlDataReader reader = cmd.ExecuteReader())
                    {
                        // Create a list to hold ArticleModel objects
                        List<ArticleModel> articles = new List<ArticleModel>();

                        // Loop through each row in the result set and create an ArticleModel object from the data
                        while (reader.Read())
                        {
                            ArticleModel article = new ArticleModel();
                            article.Title = reader.GetString("title");
                            article.Summary = reader.GetString("summary");
                            article.Link = reader.GetString("link");
                            article.Published = reader.GetDateTime("published");
                            article.Topic = reader.GetString("topic");

                            articles.Add(article);
                        }

                        // Pass the list of ArticleModel objects to the view to be displayed
                        return View(articles);
                    }
                }
            }
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
