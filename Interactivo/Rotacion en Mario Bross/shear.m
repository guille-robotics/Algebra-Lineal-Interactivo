function [new_y, new_x] = shear(angle, x, y)
% SHEAR Rotation using three shear matrices

tangent = tan(angle/2);

% Shear 1
new_x = round(x - y*tangent);
new_y = y;

% Shear 2
new_y = round(new_x*sin(angle) + new_y);

% Shear 3
new_x = round(new_x - new_y*tangent);
end

