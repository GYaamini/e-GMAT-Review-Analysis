export const processAnalysis = async(text,type) => {
    if(type == 'Commended'){
        prompt = `e-GMAT is a popular online platform for GMAT (Graduate Management Admission Test) preparation. 
        It's known for its personalized study plans, extensive video lessons, and AI-powered diagnostic tools, 
        making it a valuable resource for test takers seeking to improve their scores.
        Here is the strengths and praises in the review as content:
        Content:
        ${text}
        
        Identify and give the following in short sentences or as bullet point:
        1. Top most mentioned strengths of the platform
        2. Top features that are most appreciated by the users
        3. Mention which course result in these commendable reviews. It is mentioned in the beginning of
            each review like-
            'Online Focused:
            content and question bank
            '
        4. Overall sentiment trend
        
        Instructions:
        1. Be precise and DO NOT omit the keywords
        2. Find them by how frequently or intensely they are mentioned
        3. the available courses are Online 360, Online Focused, Mentorship, Online Intensive, and GMAT Live Prep.
        
        Analysis:
        `
    } else {
        prompt = `e-GMAT is a popular online platform for GMAT (Graduate Management Admission Test) preparation. 
        It's known for its personalized study plans, extensive video lessons, and AI-powered diagnostic tools, 
        making it a valuable resource for test takers seeking to improve their scores.
        Here is the suggested improvements or recognized flaws in the user review as content:
        Content:
        ${text}
        
        Identify and give the following in short sentences or as bullet point:
        1. Top most mentioned issues and flaws that should be addressed by the platform
        2. Top features that are bothering the users by blocking smooth learning experience
        3. Mention which course resulted these shortcomings. It is mentioned in the beginning of
            each review like-
            'Online 360:
            i feel the quant section needs to be re-evaluated.
            the estimated course durations are not accurate.
            the study plan set for me was far from realistic.
            '
        4. Overall sentiment trend
        
        Instructions:
        1. Be precise and DO NOT omit the keywords.
        2. Find them by how frequently or intensely they are mentioned.
        3. the available courses are Online 360, Online Focused, Mentorship, Online Intensive, and GMAT Live Prep.  
        
        Analysis:
        `
    }

    try{
        const res = await puter.ai.chat(
            query,
            {
                model: "meta-llama/llama-3.1-8b-instruct"
            }
        )

        return res.message.content

    } catch(firstError) {
        console.log('typing fallBack query processor...')
        try {
            const fallBackRes = await puter.ai.chat(
            query,
            {
                model: "openrouter:perplexity/sonar-reasoning"
            }
        )

        return fallBackRes.message.content

        } catch (fallBackError) {
            console.log(fallBackError)
            return "Could not process the request :/"
        }
    }
}