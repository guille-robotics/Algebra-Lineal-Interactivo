clc;
clear;

%% Read image
image = imread('mario.png');          % Load the image
image = double(image);               % Convert to double for processing

angle_deg = 45;   % User input (degrees)
angle = deg2rad(angle_deg);                 % Convert degrees to radians

cosine = cos(angle);
sine   = sin(angle);

[height, width, channels] = size(image);

%% New image dimensions
new_height = round(abs(height*cosine) + abs(width*sine)) + 1;
new_width  = round(abs(width*cosine)  + abs(height*sine)) + 1;

output = zeros(new_height, new_width, channels);

%% Image centres
original_centre_height = round(((height + 1)/2) - 1);
original_centre_width  = round(((width  + 1)/2) - 1);

new_centre_height = round(((new_height + 1)/2) - 1);
new_centre_width  = round(((new_width  + 1)/2) - 1);

%% Rotation using shear decomposition
for i = 1:height
    for j = 1:width

        % Coordinates relative to original image centre
        y = height - i - original_centre_height;
        x = width  - j - original_centre_width;

        % Apply shear transformation
        [new_y, new_x] = shear(angle, x, y);

        % Shift relative to new image centre
        new_y = new_centre_height - new_y;
        new_x = new_centre_width  - new_x;

        % Bounds check
        if new_y >= 1 && new_y <= new_height && ...
           new_x >= 1 && new_x <= new_width

            output(new_y, new_x, :) = image(i, j, :);
        end
    end
end

%% Save rotated image
output = uint8(output);
imwrite(output, 'rotated_image.png');

