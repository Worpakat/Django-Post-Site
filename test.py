def get_content_summary(content):
    """Returns content's first 10 word."""
    
    result_list = content.split()[:10]
    result_str = " ".join(result_list)
    
    return result_str 

print(get_content_summary("fer rgdfg gfhf hf ghfgh gfdf"))