# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:30:00 2021

@author: marri
"""

vector< DMatch > MatchFinder(Mat img_1, Mat img_2)
 {
int minHessian = 400;
unsigned int i;

SurfFeatureDetector detector( minHessian );

std::vector<KeyPoint> keypoints_1, keypoints_2;

detector.detect( img_1, keypoints_1 );
detector.detect( img_2, keypoints_2 );

//-- Step 2: Calculate descriptors (feature vectors)

SurfDescriptorExtractor extractor;

Mat descriptors_1, descriptors_2;

extractor.compute( img_1, keypoints_1, descriptors_1 );
extractor.compute( img_2, keypoints_2, descriptors_2 );

//-- Step 3: Matching descriptor vectors using FLANN matcher

FlannBasedMatcher matcher;

std::vector< DMatch > matches;
matcher.match( descriptors_1, descriptors_2, matches );  // ERROR

double max_dist = 0; double min_dist = 100;

//-- Quick calculation of max and min distances between keypoints
for( i = 0; i < descriptors_1.rows; i++ )
{ double dist = matches[i].distance;
if( dist < min_dist ) min_dist = dist;
if( dist > max_dist ) max_dist = dist;
}

printf("-- Max dist : %f \n", max_dist );
printf("-- Min dist : %f \n", min_dist );

//-- Draw only "good" matches (i.e. whose distance is less than 2*min_dist )
//-- PS.- radiusMatch can also be used here.
std::vector< DMatch > good_matches;

for(  i = 0; i < descriptors_1.rows; i++ )
{
  if( matches[i].distance < 2*min_dist )
{
      good_matches.push_back( matches[i]);
 }
 }

 //-- Draw only "good" matches
Mat img_matches;
drawMatches( img_1, keypoints_1, img_2, keypoints_2,
           good_matches, img_matches, Scalar::all(-1), Scalar::all(-1),
           vector<char>(), DrawMatchesFlags::NOT_DRAW_SINGLE_POINTS );

//-- Show detected matches

imshow( "Good Matches", img_matches );
ROS_INFO("size matchings: %u", good_matches.size());
for(  i = 0; i < good_matches.size(); i++ )
{
  printf( "-- Good Match [%d] Keypoint 1: %d  -- Keypoint 2: %d  \n", i, ...
good_matches[i].queryIdx, good_matches[i].trainIdx );
}

 waitKey(1);
 return good_matches;
 }