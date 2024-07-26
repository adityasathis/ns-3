function qos_metrics()
    % STEP 1: Gather configuration of the experiment
    user_terminals = [4, 8, 12];
    xlabels = {'24', '48', '72'};
    capc_configs = [0, 2];
    num_runs = 4;
    trafficModel = 0;
    num = 2;
    bw = 80;
    simTime = 5;

    % STEP 2: Initialize cell arrays to store results
    throughput_guarantees0 = cell(1, length(capc_configs));
    throughput_guarantees1 = cell(1, length(capc_configs));
    throughput_guarantees2 = cell(1, length(capc_configs));
    throughput_guarantees3 = cell(1, length(capc_configs));
    delay_guarantees0 = cell(1, length(capc_configs));
    delay_guarantees1 = cell(1, length(capc_configs));
    delay_guarantees2 = cell(1, length(capc_configs));
    delay_guarantees3 = cell(1, length(capc_configs));
    throughput_ci0 = cell(1, length(capc_configs));
    throughput_ci1 = cell(1, length(capc_configs));
    throughput_ci2 = cell(1, length(capc_configs));
    throughput_ci3 = cell(1, length(capc_configs));
    delay_ci0 = cell(1, length(capc_configs));
    delay_ci1 = cell(1, length(capc_configs));
    delay_ci2 = cell(1, length(capc_configs));
    delay_ci3 = cell(1, length(capc_configs));

    % STEP 3: Iterate over each user terminal and calculate QoS metrics for multiple runs
    for ut = user_terminals
        for mode = capc_configs
            if mode == 0
                capc = 0;
                scheduler = 'PF';
                lcScheduler = 0;
            elseif mode == 1
                capc = 0;
                scheduler = 'Qos';
                lcScheduler = 1;
            else
                capc = 1;
                scheduler = 'Qos';
                lcScheduler = 1;
            end

            disp(['Running for Mode: ', num2str(mode), ' and UT: ', num2str(ut)])

            file_paths = arrayfun(@(i) sprintf('nru-csv/ip/changeuts-gnb6-ap0-ut%d-ratio1111-numerology%d-bandwidth%d-scheduler%s-lcScheduler%d-trafficModel%d-capc%d-simtime%d-run%d.csv', ut, num, bw, scheduler, lcScheduler, trafficModel, capc, simTime, i), 0:num_runs-1, 'UniformOutput', false);
            throughputs0 = [];
            throughputs1 = [];
            throughputs2 = [];
            throughputs3 = [];
            delays0 = [];
            delays1 = [];
            delays2 = [];
            delays3 = [];
            % disp(file_paths);
            for file_path = file_paths
                [throughput0, throughput1, throughput2, throughput3, delay0, delay1, delay2, delay3] = calculate_qos_metrics(file_path{1});
                throughputs0 = [throughputs0; throughput0];
                throughputs1 = [throughputs1; throughput1];
                throughputs2 = [throughputs2; throughput2];
                throughputs3 = [throughputs3; throughput3];

                delays0 = [delays0; delay0];
                delays1 = [delays1; delay1];
                delays2 = [delays2; delay2];
                delays3 = [delays3; delay3];
            end

            throughput_guarantees0{capc+1} = [throughput_guarantees0{capc+1}, mean(throughputs0)];
            throughput_guarantees1{capc+1} = [throughput_guarantees1{capc+1}, mean(throughputs1)];
            throughput_guarantees2{capc+1} = [throughput_guarantees2{capc+1}, mean(throughputs2)];
            throughput_guarantees3{capc+1} = [throughput_guarantees3{capc+1}, mean(throughputs3)];

            delay_guarantees0{capc+1} = [delay_guarantees0{capc+1}, mean(delays0)];
            delay_guarantees1{capc+1} = [delay_guarantees1{capc+1}, mean(delays1)];
            delay_guarantees2{capc+1} = [delay_guarantees2{capc+1}, mean(delays2)];
            delay_guarantees3{capc+1} = [delay_guarantees3{capc+1}, mean(delays3)];
            disp(['DelayGuarantees0: ', num2str(delay_guarantees0{capc+1})])
            disp(['DelayGuarantees1: ', num2str(delay_guarantees1{capc+1})])
            disp(['DelayGuarantees2: ', num2str(delay_guarantees2{capc+1})])
            disp(['DelayGuarantees3: ', num2str(delay_guarantees3{capc+1})])

            throughput_ci0{capc+1} = [throughput_ci0{capc+1}, std(throughputs0)/sqrt(length(throughputs0)) * tinv(0.975, length(throughputs0) - 1)];
            throughput_ci1{capc+1} = [throughput_ci1{capc+1}, std(throughputs1)/sqrt(length(throughputs1)) * tinv(0.975, length(throughputs1) - 1)];
            throughput_ci2{capc+1} = [throughput_ci2{capc+1}, std(throughputs2)/sqrt(length(throughputs2)) * tinv(0.975, length(throughputs2) - 1)];
            throughput_ci3{capc+1} = [throughput_ci3{capc+1}, std(throughputs3)/sqrt(length(throughputs3)) * tinv(0.975, length(throughputs3) - 1)];

            delay_ci0{capc+1} = [delay_ci0{capc+1}, std(delays0)/sqrt(length(delays0)) * tinv(0.95, length(delays0) - 1)];
            delay_ci1{capc+1} = [delay_ci1{capc+1}, std(delays1)/sqrt(length(delays1)) * tinv(0.95, length(delays1) - 1)];
            delay_ci2{capc+1} = [delay_ci2{capc+1}, std(delays2)/sqrt(length(delays2)) * tinv(0.95, length(delays2) - 1)];
            delay_ci3{capc+1} = [delay_ci3{capc+1}, std(delays3)/sqrt(length(delays3)) * tinv(0.95, length(delays3) - 1)];
        end
    end

    % Plotting the results
    x = 1:length(xlabels);  % the label locations
    width = 0.4;  % the width of the bars

    figure;
    % Plot for Delay Guarantees vs User Terminals for QoS class 0
    subplot(2,2,1);
    bar(x - width/2, delay_guarantees0{1}, width, 'FaceColor', 'b');
    hold on;
    bar(x + width/2, delay_guarantees0{2}, width, 'FaceColor', 'r');
    yline(5, '--', '5QI 88 Packet Delay Budget (10ms)', 'Color', 'r');
    errorbar(x - width/2, delay_guarantees0{1}, delay_ci0{1}, 'k.', 'LineWidth', 1.5);
    errorbar(x + width/2, delay_guarantees0{2}, delay_ci0{2}, 'k.', 'LineWidth', 1.5);
    hold off;
    set(gca, 'XTick', x, 'XTickLabel', xlabels);
    xlabel('User Terminals Per gNB', 'FontSize', 16);
    ylabel('Average Delay (ms)', 'FontSize', 16);
    legend({'Static CAPC with PF Scheduler', 'Decoupled CAPC'}, 'FontSize', 16);
    grid on;

    % Plot for Delay Guarantees vs User Terminals for QoS class 1
    subplot(2,2,2);
    bar(x - width/2, delay_guarantees1{1}, width, 'FaceColor', 'b');
    hold on;
    bar(x + width/2, delay_guarantees1{2}, width, 'FaceColor', 'r');
    yline(150, '--', '5QI 2 Packet Delay Budget (150ms)', 'Color', 'r');
    errorbar(x - width/2, delay_guarantees1{1}, delay_ci1{1}, 'k.', 'LineWidth', 1.5);
    errorbar(x + width/2, delay_guarantees1{2}, delay_ci1{2}, 'k.', 'LineWidth', 1.5);
    hold off;
    set(gca, 'XTick', x, 'XTickLabel', xlabels);
    xlabel('User Terminals in Scenario', 'FontSize', 16);
    ylabel('Average Delay (ms)', 'FontSize', 16);
    legend({'Static CAPC with PF Scheduler', 'Decoupled CAPC'}, 'FontSize', 16);
    grid on;

    % Plot for Delay Guarantees vs User Terminals for QoS class 2
    subplot(2,2,3);
    bar(x - width/2, delay_guarantees2{1}, width, 'FaceColor', 'b');
    hold on;
    bar(x + width/2, delay_guarantees2{2}, width, 'FaceColor', 'r');
    yline(300, '--', '5QI 4 Packet Delay Budget (300ms)', 'Color', 'r');
    errorbar(x - width/2, delay_guarantees2{1}, delay_ci2{1}, 'k.', 'LineWidth', 1.5);
    errorbar(x + width/2, delay_guarantees2{2}, delay_ci2{2}, 'k.', 'LineWidth', 1.5);
    hold off;
    set(gca, 'XTick', x, 'XTickLabel', xlabels);
    xlabel('User Terminals in Scenario', 'FontSize', 16);
    ylabel('Average Delay (ms)', 'FontSize', 16);
    legend({'Static CAPC with PF Scheduler', 'Decoupled CAPC'}, 'FontSize', 16);
    grid on;

    % Plot for Delay Guarantees vs User Terminals for QoS class 3
    subplot(2,2,4);
    bar(x - width/2, delay_guarantees3{1}, width, 'FaceColor', 'b');
    hold on;
    bar(x + width/2, delay_guarantees3{2}, width, 'FaceColor', 'r');
    % yline(50, '--', '5QI 82 Packet Delay Budget (50ms)', 'Color', 'r');
    errorbar(x - width/2, delay_guarantees3{1}, delay_ci3{1}, 'k.', 'LineWidth', 1.5);
    errorbar(x + width/2, delay_guarantees3{2}, delay_ci3{2}, 'k.', 'LineWidth', 1.5);
    hold off;
    set(gca, 'XTick', x, 'XTickLabel', xlabels);
    xlabel('User Terminals in Scenario', 'FontSize', 16);
    ylabel('Average Delay (ms)', 'FontSize', 16);
    legend({'Static CAPC with PF Scheduler', 'Decoupled CAPC'}, 'FontSize', 16);
    grid on;
end

function [throughput0, throughput1, throughput2, throughput3, delay0, delay1, delay2, delay3] = calculate_qos_metrics(file_path)
    data = readtable(file_path, 'Format', '%s%s%f%f%f%f%f%f');
    data.Properties.VariableNames = {'Type', 'TypeDetail', 'QosThroughput', 'QosDelay', 'TxPackets', 'RxPackets', 'AchievedThroughput', 'AchievedDelay'};

    % Get filtered data for individual traffic classes
    filtered_data_0 = data(data.QosThroughput == 3e+7   & data.QosDelay == 5   & (data.RxPackets/data.TxPackets) > 0, :);
    filtered_data_1 = data(data.QosThroughput == 5e+6   & data.QosDelay == 150 & (data.RxPackets/data.TxPackets) > 0, :);
    filtered_data_2 = data(data.QosThroughput == 5e+6   & data.QosDelay == 300 & (data.RxPackets/data.TxPackets) > 0, :);
    filtered_data_3 = data(data.QosThroughput == 0      & data.QosDelay == 0   & (data.RxPackets/data.TxPackets) > 0, :);


    % Calculate the weighted average throughput of all packets
    % sum(rxPackets*achievedThroughput)/sum(rxPackets)
    % for every traffic class
    throughput0 = sum(filtered_data_0.RxPackets .* filtered_data_0.AchievedThroughput) / sum(filtered_data_0.RxPackets);
    throughput1 = sum(filtered_data_1.RxPackets .* filtered_data_1.AchievedThroughput) / sum(filtered_data_1.RxPackets);
    throughput2 = sum(filtered_data_2.RxPackets .* filtered_data_2.AchievedThroughput) / sum(filtered_data_2.RxPackets);
    throughput3 = sum(filtered_data_3.RxPackets .* filtered_data_3.AchievedThroughput) / sum(filtered_data_3.RxPackets);

    % Calculate the delays
    % sum(rxPackets*achievedDelay)/sum(rxPackets)
    % for every traffic class
    % delay0 = sum(filtered_data_0.RxPackets .* filtered_data_0.AchievedDelay) / sum(filtered_data_0.RxPackets);
    % delay1 = sum(filtered_data_1.RxPackets .* filtered_data_1.AchievedDelay) / sum(filtered_data_1.RxPackets);
    % delay2 = sum(filtered_data_2.RxPackets .* filtered_data_2.AchievedDelay) / sum(filtered_data_2.RxPackets);
    % delay3 = sum(filtered_data_3.RxPackets .* filtered_data_3.AchievedDelay) / sum(filtered_data_3.RxPackets);
    delay0 = sum(filtered_data_0.AchievedDelay) / length(filtered_data_0.AchievedDelay);
    delay1 = sum(filtered_data_1.AchievedDelay) / length(filtered_data_1.AchievedDelay);
    delay2 = sum(filtered_data_2.AchievedDelay) / length(filtered_data_2.AchievedDelay);
    delay3 = sum(filtered_data_3.AchievedDelay) / length(filtered_data_3.AchievedDelay);
    
    % Display the results
    % disp(['Weighted Average Throughput for Traffic Class 0: ', num2str(throughput0)])
    % disp(['Weighted Average Throughput for Traffic Class 1: ', num2str(throughput1)])
    % disp(['Weighted Average Throughput for Traffic Class 2: ', num2str(throughput2)])
    % disp(['Weighted Average Throughput for Traffic Class 3: ', num2str(throughput3)])
    disp(['Weighted Average Delay for Traffic Class 0: ', num2str(delay0)]);
    disp(['Weighted Average Delay for Traffic Class 1: ', num2str(delay1)]);
    disp(['Weighted Average Delay for Traffic Class 2: ', num2str(delay2)]);
    disp(['Weighted Average Delay for Traffic Class 3: ', num2str(delay3)]);
end
