using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using System.Diagnostics;
using System.Xml;
using System.IO;

namespace WebApplication1.Controllers

{
    //[Authorize]
    public class ValuesController : ApiController
    {
        // GET api/values
        public IEnumerable<string> Get()
        {
            return new string[] { "value1", "value2" };
        }

        // GET api/values/5
        public string Get(String id)
        {
            // NO XSS
            return id;
            //return Request.Headers.ToString();

            // Command INjection
            /*
            string input = id;
            ProcessStartInfo startInfo = new ProcessStartInfo("cmd.exe");
            startInfo.WindowStyle = ProcessWindowStyle.Normal;
            startInfo.Arguments = "/c " + input;
            Process p = Process.Start(startInfo);
            return p.StandardOutput.ReadToEnd();
            */


        }

        // POST api/values
        public String Post(HttpRequestMessage request)
        {
            // NO XXE
            XmlReaderSettings rs = new XmlReaderSettings();
            
            //rs.DtdProcessing = DtdProcessing.Parse;

            XmlReader myReader = XmlReader.Create(new StringReader(request.Content.ReadAsStringAsync().Result));
            String s="";

            while (myReader.Read())
            {
                s+=myReader.Value;
            }
            return s;
       }

        // PUT api/values/5
        public void Put(int id, [FromBody]string value)
        {
        }

        // DELETE api/values/5
        public void Delete(int id)
        {
        }
    }
}
