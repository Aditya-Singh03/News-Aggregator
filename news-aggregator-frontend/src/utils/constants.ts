import { PostInfo } from "@/types";

const BACKEND_URL: string = "http://localhost:8000";

const RECOMMENDER_URL: string = "something";

const TOPICS: Array<string> = [
  "World News",
  "National News",
  "Business & Finance",
  "Science & Technology",
  "Health & Wellness",
  "Entertainment & Culture",
  "Sports",
  "Travel",
  "Politics",
  "Education",
  "Environment & Sustainability",
  "Arts & Literature",
  "Gaming & Esports",
  "Food & Cooking",
  "Fashion & Beauty",
  // Specific Interests can be nested within these categories
  "Local News",
  "Personal Finance",
  "Science by Field",
  "Health Conditions",
  "Hobbies & Interests",
  "Social Issues",
];

const SAMPLE_POSTS: PostInfo[] = [
  {
    id: "xxxxxyyyyy",
    title: "Post Title",
    link: "link_to_post",
    date: "post data",
    media: "media post has",
    author: "author",
    upvotes: 69100,
    downvotes: 70000,
  },{
    id: "xxxxxyyyyy",
    title: "Post Title",
    link: "link_to_post",
    date: "post data",
    media: "media post has",
    author: "author",
    upvotes: 69100,
    downvotes: 70000,
  },{
    id: "xxxxxyyyyy",
    title: "Post Title",
    link: "link_to_post",
    date: "post data",
    media: "media post has",
    author: "author",
    upvotes: 69100,
    downvotes: 70000,
  },{
    id: "xxxxxyyyyy",
    title: "Post Title",
    link: "link_to_post",
    date: "post data",
    media: "media post has",
    author: "author",
    upvotes: 69100,
    downvotes: 70000,
  }
  
];
export { BACKEND_URL, RECOMMENDER_URL, TOPICS, SAMPLE_POSTS };
