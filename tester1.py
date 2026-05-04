# Download all the 3 python files and the tester.sh files and run the shell script by - ./tester.sh
# LLM and codeChunksHelper
# tests LLM And gets sample response for the query statment
# tests code chunks helper and gives function name

def test_llm():
    try:
        from LLM import run_model
        print("------------------------------------------------------------------------")
        print("Testing LLM...")
        #print("------------------------------------------------------------------------")
        response = run_model("Context about pandas", "Give details about pandas")
        if response:
            #print("------------------------------------------------------------------------")
            print(f"Pass - LLM ran successfully, response: {response[:200]}...")  # Truncate for brevity
            print("------------------------------------------------------------------------")
        else:
            print("------------------------------------------------------------------------")
            print("Fail - LLM: No response generated.")
            print("------------------------------------------------------------------------")
    except Exception as e:
        print(f"Fail - LLM: {e}")

def test_code_chunks_helper():
    try:
        from codechunksHelper import extract_function_name
        print("------------------------------------------------------------------------")
        print("Testing codeChunksHelper...")
        #print("------------------------------------------------------------------------")
        function_name = extract_function_name("def test_function(): pass")
        if function_name == "test_function":
            #print("------------------------------------------------------------------------")
            print(f"Pass - Extracted function name: {function_name}")
            print("------------------------------------------------------------------------")
        else:
            print("------------------------------------------------------------------------")
            print(f"Fail - Incorrect function name: {function_name}")
            print("------------------------------------------------------------------------")
    except Exception as e:
        print(f"Fail - codeChunksHelper: {e}")

if __name__ == "__main__":
    test_llm()
    test_code_chunks_helper()
