/**
* Basic example of creating a stand alone program linked against Connector/C++
*
* This example is not integrated into the Connector/C++ build environment.
* You must run "make install" prior to following the build instructions
* given here.
*
* To compile the standalone example on Linux try something like:
*
* /usr/bin/c++
*   -o standalone
*   -I/usr/local/include/cppconn/
*   -Wl,-Bdynamic -lmysqlcppconn
*    examples/standalone_example.cpp
*
* To run the example on Linux try something similar to:
*
*  LD_LIBRARY_PATH=/usr/local/lib/ ./standalone
*
* or:
*
*  LD_LIBRARY_PATH=/usr/local/lib/ ./standalone host user password database

to build:
g++  -lmysqlcppconn cpp_mysql_client.cpp ; ./a.out

for help:
http://blog.csdn.net/abcjennifer/article/details/16983929

*/


/* Standard C++ includes */
#include <stdlib.h>
#include <iostream>
#include <string.h>
#include <sstream>
#include <vector>
#include <stdexcept>
#include <time.h>
#include <map>
#include "mysql_connection.h"
#include "mysql_driver.h"

#include <boost/algorithm/string.hpp>

#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>

#define EXAMPLE_HOST "localhost"
#define EXAMPLE_USER "root"
#define EXAMPLE_PASS "roo"
#define EXAMPLE_DB "by_work"


using namespace std;
using namespace sql;
using namespace sql::mysql;
typedef pair<string, int> PAIR;
bool cmp_by_value(const PAIR& lhs, const PAIR& rhs) {
	return lhs.second > rhs.second;
}

int main(int argc, const char **argv)
{
	string url(argc >= 2 ? argv[1] : EXAMPLE_HOST);
	const string user(argc >= 3 ? argv[2] : EXAMPLE_USER);
	const string pass(argc >= 4 ? argv[3] : EXAMPLE_PASS);
	const string database(argc >= 5 ? argv[4] : EXAMPLE_DB);
	clock_t start, end;
	try {
		Driver * driver = sql::mysql::get_driver_instance();
		/* Using the Driver to create a connection */
		auto_ptr< sql::Connection > con(driver->connect(url, user, pass));
		con->setSchema(database);
		auto_ptr< sql::Statement > stmt(con->createStatement());
		string word_input;
		string query = "SELECT * from all_info where word =";
		map<string, int >word_count_map;
		map<string, int>::iterator it;
		vector<PAIR>::iterator vec_it;
		stringstream ss;
		string word_set;
		int num;
		vector<string> tokens;

		while (cout << "请输入要查询的词汇:")
		{
			cin >> word_input;
			start = clock();
			auto_ptr< sql::ResultSet > res(stmt->executeQuery(query + "\"" + word_input + "\""));

			while (res->next()) {
				// string word = res->getString("word");
				// string month = res->getString("month");
				word_set = res->getString("word_set");
				// boost::trim(word_set);
				//0.003
				boost::split(tokens, word_set, boost::is_any_of(" "));
				//0.55
				for (size_t i = 0; i < tokens.size(); i += 2)
				{
					it = word_count_map.find(tokens[i]);
					if (it == word_count_map.end())
					{
						word_count_map[tokens[i]] = 0;
					}
					//1.15
					// cout << tokens[i + 1] << endl;
					ss << tokens[i + 1]; //从str输入
					ss >> num; //输出到int
					ss.clear();
					word_count_map[tokens[i]] += num;
				}
			}
			//1.885
			end = clock();
			printf("sql时间:%f\n", double(end - start) / CLOCKS_PER_SEC);
			// continue;


			start = clock();
			vector<PAIR> word_count_vec(word_count_map.begin(), word_count_map.end());
			word_count_map.clear();
			sort(word_count_vec.begin(), word_count_vec.end(), cmp_by_value);
			num = 0;
			for (vec_it = word_count_vec.begin(); vec_it != word_count_vec.end(); ++vec_it) {
				if (vec_it->first == word_input)
					continue;
				if (num < 20)
					cout << vec_it->first << " " << vec_it->second << endl;
				num += 1;
			}
			end = clock();
			printf("计算时间:%f\n", double(end - start) / CLOCKS_PER_SEC);
		}
		return 0;

	} catch (sql::SQLException &e) {
		/*
		The MySQL Connector/C++ throws three different exceptions:

		- sql::MethodNotImplementedException (derived from sql::SQLException)
		- sql::InvalidArgumentException (derived from sql::SQLException)
		- sql::SQLException (derived from runtime_error)
		*/
		cout << "# ERR: SQLException in " << __FILE__;
		//cout << "(" << EXAMPLE_FUNCTION << ") on line " << __LINE__ << endl;
		/* Use what() (derived from runtime_error) to fetch the error message */
		cout << "# ERR: " << e.what();
		cout << " (MySQL error code: " << e.getErrorCode();
		cout << ", SQLState: " << e.getSQLState() << " )" << endl;

		return EXIT_FAILURE;
	}

	return EXIT_SUCCESS;
}








