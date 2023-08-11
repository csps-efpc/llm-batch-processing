# Our sole external import is nomic.ai's GPT4All
from gpt4all import GPT4All

# We also import the core json and regular expressions libraries
import json
import re

# The information to be prosessed is loaded into memory. JSON is used here for simplicity; you can use a 
# database, API, search engine results, or whatever else suits your use case.
data = json.load(open("./input.json"))

# We instantiate our LLM. For this example we use airoboros-l2 because it is very compliant for "context obediant
# question answering". airoboros-l2 is also a very good general-purpose LLM.
model = GPT4All("airoboros-l2-7b-gpt4-m2.0.ggmlv3.q4_0.bin", n_threads = 4, model_path='.') 

# We iterate over each element in the retrieved data, and process the ones that pass a simple data quality check.
for idx, row in enumerate(data):
     if(("desc_en" in row) and row["desc_en"]):
         # We open a new chat session with the LLM for each element being considered. The prompt template is 
         # specific to the model, and can be found on the model card. In this case, we're adding a simple metadata 
         # and text context. Note that the longer the content in the preamble, the longer it takes for the model
         # to start generating tokens. Also note that each model has a maximum "token window" that it supports. 
         # Your input prompt and the output should stay below this size. An English or French word is typically 
         # about 1.3 tokens.
         with model.chat_session(prompt_template = """BEGININPUT BEGINCONTEXT
[course: """ +row["id"]+  """]
ENDCONTEXT
"""+row["desc_en"]+"""
ENDINPUT
BEGININSTRUCTION
{0}
ENDINSTRUCTION
"""):
             # Here, we actually submit our question about the content to the model. This step is computationally
             # *very* expensive. Expect calls to take 20-30 seconds each.  
             output = model.generate("For course "+row["id"]+", write a numbered list of the top 5 types of federal public servants that would most benefit from this course.")
             print(output)
             # To get the structure out, we do some old-fashioned output massaging to extract the list that the model generated.
             # We create the array that will hold the output features.
             outputFeatures = [];
             # First we trim any whitespace from either end
             output = output.strip(' \t\r\n')
             # Then we break the output up into lines.
             lines = output.splitlines();
             # There are two patterns that come out of the models. Single-line numbered lists, and multi-line lists with different markers. We handle single-line output first.
             if(len(lines) == 1):
                 # does the one-liner start right away, or is there frontmatter to delete?
                 startsWithDigit = lines[0][0].isdigit()
                 # We break the list up at the numbers.
                 lines = re.split(r'[\d]+.', lines[0])
                 # If the list didn't start with the first item (ie. The model emitted frontmatter like "Here's 
                 # the list you asked for:"), we trim the frontmatter.
                 if(not startsWithDigit):
                     del lines[0];
                 # Next, we trim the numbers or bullets from the output, and populate the output features.
                 for line in lines:
                     line = line.strip(' 1234567890.-·')
                     print(row["id"] + ": " + line)
                     outputFeatures.append(line)
             # Next, we treat the case of multi-line lists:
             else:
                 for line in lines:
                     # We treat any line that starts with a bullet or digit as an item to be output.
                     if(line and ( line[0].isdigit() or line[0] == '-' 
or line[0] == '·')):
                         # We trim off the bullets and spaces, and add the content to the output features.
                         line = line.strip(' 1234567890.-·')
                         print(row["id"] + ": " + line)
                         outputFeatures.append(line)
             # At the end of each input data element, we act on the output that has been parsed. In this case,
             # We add the features back to the data model.
             row['audience_en'] = outputFeatures 
# Finally, we write the updated data model out to a file.
with open("./output.json", "w") as write_file:
     json.dump(data, write_file, indent=4)


