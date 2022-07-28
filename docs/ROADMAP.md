## TODO plan
### Architectural tasks
    1. SSDEEP responsese check - DONE(with mean ans std, may be extend)
    2. Reply time check - session tracking(e.g. for python requests package)
    3. Mark both 1,2 as suspicious if stats has anomalies
    4. Add feature for starting fuzing process in parrallel:
        4.1 Add possibility to handle several files in several threads
    5. Add parameters from other hints and services
        merge parameters from other hints and services, other variant /|\
    6. Additional tasks:
        types refactoring - make named tuple where required
    7. Save data results during fuzzing

### Business logic tasks
    1. Make single k_v_Fuzzy object(mix to basic json sometimes <-- this case) OR test_method mix_it_sometimes
    2. Semantic mutation:  --> HARD
        4.1 action mytator by mutation testig tools(extract code or use tool as is to get mutated code bundle)
        4.2 JSON mutator - big project with semantic mutation, many questions how to realize
    3. Add structed mutations(testing with structly-correct random data input)
    4. Try to realize Lamport timestamp for services to get error information
    5. I'm lucky parameter
    6. susp_replies={"status: [-404], "body": ["{"success": true}"]}

### Routine tasks
    1. Recursively decrease delay between 500s for second check
    2. Add option for adding dir with custom generators/mutators
        First, post_json_fuzzer will try to find and registrate those generators in those folders
    
    4. Add jupiter notebook description for project
    5. After merge tm params, make every tm to have its own susp request(e.g. pair_wise[200, 404] | miss_it[200, 204])

### Tasks for future
    1. From string import Template - try to replace str(dict)/smart_replace and others by substitute operation
    2. Check if Python is > 3.6 because of potential using of named tuples
    3. Add parameter for pair_wise(combine with fuzzy with spesific index)
    4. Pay attention to Dharma fuzzer

### Thoughts
    1. All items in data_set items MUST be invalid, and only default value should be valid.
        This is important because we need to get json bodies with only wrong values
    2. Try to apply a genetic algorithm to function fuzzing, i.e. mutate operators,
        add idempotent operations according to the rules of the genetic algorithm
    3. Idempotent functions for ast mutator will give coverage larger than just using basic function mutation?
    4. Add method for checking if API is fuzzable(has RPS > N without deadlocks, other errors)
        It could be made in statistical approach: add 'test' method for check if num of 5XXs is smaller than 1/100
        of all sent test requests(e.g.)
    5. AST-based action mutations - is it the structure based mutation?
        Can it be coverage guided? Function-based mutation(actions by JS or Nikita) - is closer to semantic mutation?
    6. I need to check if there is a project that allows to create functions that produces the same result
        as current function(for making several variants of functions which I can use for mutate operations within ast)
    7. Try to make decorator with request parameters for pytest requests via post_json_fuzzer
        (e.g. @params(headers={"one":1, "two": 2}def send_fuzz_requests() ...))
    8. Watch which bugs are fixed and fuzz all combinations of fixes mentioned on GL


### DONE for sync requests
    optionally save results as ready curl requests, deep info logs

### DONE, but not tested
    For every fuzzy(for deep info log puropses) we need the description(e.g. what protobuf/grpc data in the current fuzzy could be)

### DONE
    Add the possibility not to add data_set(in case when we just use MISS_IT test-method so there is no need to fuzz default value) - DONE
    add fuzzer.log file with deep log info - DONE
    Try to addd lazy generator (e.g. random_every_time) with all other params which could be e.g. pairwise
        (id will make different random numbers: "id": 1928399182, "test": 1, "id": 9898934982034, "test": 2, etc.)
    add turm_on flag(if it is false, the current fuzzy does not participate in fuzzing)
    add pm for use this parameter in every test neverless other parameters pms(take_curr_and_others_by_their_test_method)
    *get_pack_by_methods("client_id", [list_once, list_several_times])
    Make sure that all items in tape are unique
    Attach file with patterns for fuzzing
    Add terms:
        tape, metadata, fuzzy, deck(jsons with add_data ready to send)
    Realize 1) lack of current parameter and 2) doubled one
           can be realized easy with
            1) Fuzzy itself with any dataset value wich differs from base one
            2) One mode Fuzzy with all required params for current JSON in corresponding place
               (e.g. for clientid create another dummy Fuzzy with "dummy" default name and clientid in dataset)