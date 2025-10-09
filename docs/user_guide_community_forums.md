# User Guide: Community Forums

*Документація також доступна українською мовою: [user_guide_community_forums_uk.md](user_guide_community_forums_uk.md)*

## Overview
This guide explains how to use GlobalScope MultiFrame's Community Forums to participate in technical discussions, receive community support, share knowledge, and engage in industry discussions. The forums provide a structured platform for collective problem-solving and experience sharing among chip designers.

## Prerequisites
- Completed [Platform Overview and Architecture](user_guide_platform_overview.md)
- Basic understanding of forum and discussion concepts
- Familiarity with [Family Collaboration](user_guide_family_collaboration.md)
- Access to appropriate project resources and permissions

## Understanding Community Forums

### What are Community Forums?
Community Forums are GlobalScope MultiFrame's structured discussion platform that enables:
- **Technical Discussions**: In-depth discussions on design challenges and solutions
- **Community Support**: Collective problem-solving and question answering
- **Knowledge Sharing**: Dissemination of best practices and methodologies
- **Industry News**: Updates on trends and innovations
- **Collaboration**: Finding partners for projects and research

### Forum Features
The Community Forums offer several key capabilities:
- **Categorized Discussions**: Thematic sections for different topics
- **Search and Filtering**: Efficient finding of relevant information
- **Rating System**: Mechanisms for evaluating message usefulness
- **Notifications**: Automatic alerts for new replies
- **Moderation**: Quality management and rule compliance

## Navigating the Forums

### 1. Accessing Forums
1. Navigate to the "Collaboration" module from the main navigation
2. Click on "Community Forums" in the left sidebar
3. Browse the list of available forum categories

### 2. Category Overview
Forums are organized into several key categories:
- **Chip Design**: Technical aspects of design discussions
- **Software**: Questions about tools and CAD
- **Fabrication**: Manufacturing technologies and fabrication
- **Web3 and Security**: Blockchain and quantum security discussions
- **Career and Learning**: Employment opportunities and professional development
- **Announcements**: New platform features and updates

### 3. Searching for Information
Efficiently find the information you need:
- **Global Search**: Use the search bar to search across all forums
- **Filters**: Narrow results by date, popularity, or status
- **Tags**: Use tags to find related discussions
- **Bookmarks**: Save important topics for quick access

## Participating in Discussions

### 1. Creating New Topics
Create engaging discussions:
1. Select the appropriate forum category
2. Click the "New Topic" button
3. Enter a clear topic title
4. Write a comprehensive description of the question or topic
5. Add relevant tags for better classification
6. Click "Publish"

### 2. Replying to Posts
Participate in existing discussions:
- **Helpful Responses**: Provide accurate and justified answers
- **Quoting**: Use quoting to reference previous messages
- **Formatting**: Use formatting to improve readability
- **Attachments**: Attach code, images, or documents as needed

### 3. Voting and Rating
Help the community identify useful content:
- **Likes**: Mark useful messages
- **Dislikes**: Flag inaccurate or unnecessary information
- **Accepted Answers**: Topic authors can mark the best answers
- **Reports**: Report rule violations or spam

## Managing Your Discussions

### 1. Tracking Topics
Stay updated on activity in your discussions:
- **Subscriptions**: Automatically receive notifications for new replies
- **Unread Topics**: Quickly find topics with new messages
- **Private Messages**: Receive notifications for mentions and replies

### 2. Editing Content
Maintain the accuracy of your content:
- **Editing Posts**: Update your messages when needed
- **Deleting Topics**: Remove your topics if they're no longer relevant
- **Edit History**: Track changes to your messages

### 3. Notification Settings
Customize notifications according to your preferences:
- **Notification Frequency**: Choose how often to receive updates
- **Notification Types**: Select what you want to be notified about
- **Email Notifications**: Enable or disable email notifications

## Moderation and Quality

### 1. Community Guidelines
Follow established rules for quality discussions:
- **Respect Others**: Avoid offensive or discriminatory comments
- **Be Specific**: Provide accurate and useful information
- **Avoid Spam**: Don't post advertisements or unrelated content
- **Use Proper Categories**: Post topics in appropriate sections

### 2. Community Moderation
Help maintain discussion quality:
- **Reporting to Moderators**: Report rule violations
- **Duplicate Tracking**: Check for similar topics before creating new ones
- **Constructive Criticism**: Provide useful feedback
- **Supporting Newcomers**: Help new participants get settled

### 3. Expert Recognition
Receive recognition for your community contributions:
- **Reputation System**: Earn points for helpful answers
- **Badges and Awards**: Receive badges for activity
- **Expert Status**: Become a recognized expert in certain fields
- **Special Privileges**: Gain additional capabilities for activity

## Best Practices

### Forum Participation
1. Search for existing discussions before creating a new topic
2. Use clear topic titles and detailed problem descriptions
3. Provide sufficient context for understanding your question
4. Share solutions if you find an answer to your question
5. Be grateful for help and polite in all interactions

### Creating Quality Content
1. Use formatting to improve message readability
2. Add code examples, diagrams, and screenshots when needed
3. Provide sources or links to additional information
4. Mark resolved topics to help other users
5. Update information if it becomes outdated

### Community Support
1. Help newcomers navigate the platform
2. Share your experience and knowledge with others
3. Participate in moderation by reporting violations
4. Foster constructive discussions
5. Support a positive atmosphere on the forums

## Troubleshooting

### Common Issues and Solutions

#### Issue: Not receiving notifications for new replies
- **Cause**: Incorrect notification settings or unsubscribed from topic
- **Solution**: Check notification settings in your profile and ensure you're subscribed to the topic

#### Issue: Can't find appropriate category for my topic
- **Cause**: Insufficient categories or unclear classification
- **Solution**: Use global search or contact moderators with a proposal for a new category

#### Issue: My topic isn't getting responses
- **Cause**: Insufficient problem description or wrong category
- **Solution**: Improve the problem description, add more context, and check category correctness

#### Issue: Encountering unacceptable content or behavior
- **Cause**: Community rules violations by other users
- **Solution**: Use the reporting function to notify moderators

#### Issue: Delays in forum page loading
- **Cause**: Network issues or high server load
- **Solution**: Check your internet connection or try again later

## Related Features
- [Platform Overview and Architecture](user_guide_platform_overview.md)
- [Family Collaboration](user_guide_family_collaboration.md)
- [Designer Network](user_guide_designer_network.md)
- [Global Chat](user_guide_global_chat.md)

## API Reference
For programmatic community forum management, refer to the following API endpoints:
- `GET /api/v1/community-forums/categories` - Get list of forum categories
- `GET /api/v1/community-forums/categories/{category_id}/topics` - Get topics in category
- `POST /api/v1/community-forums/topics` - Create new topic
- `GET /api/v1/community-forums/topics/{topic_id}` - Get topic details
- `POST /api/v1/community-forums/topics/{topic_id}/posts` - Add post to topic
- `PUT /api/v1/community-forums/posts/{post_id}` - Update post

For detailed API documentation, see [API Documentation](api_documentation.md).